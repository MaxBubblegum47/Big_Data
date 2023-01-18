# Prima query 
UFFICIALE - Quali sono gli utenti piu' influenti all'interno del grafo

CALL gds.graph.project.cypher(
'twitter-user',
'MATCH (u:User) return id(u) as id',
'MATCH (u1:User)-[:POST]->(:Tweet)<-[:RETWEETED]-(:Tweet)<-[:POSTED]-(u2:User) 
RETURN id(u2) as source, id(u1) as target
UNION
MATCH (r1:Troll)-[:POSTED]->(:Tweet)<-[:RETWEETED]-(:Tweet)<-[:POSTED]-(r2:Troll)  
RETURN id(r2) as source, id(r1) as target
UNION
MATCH (u1:User)<-[:MENTION]-(t:Tweet)<-[:POST]-(u2:User)
RETURN id(u2) as source, id(u1) as target
UNION
MATCH (t1:Troll)<-[:MENTION]-(t:Tweet)<-[:POST]-(t2:Troll)
RETURN id(t2) as source, id(t1) as target',
{validateRelationships: false})

CALL gds.degree.stream('twitter-user')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).screen_name AS name, score 
ORDER BY score DESC LIMIT 10;


stima del mutate
CALL gds.degree.mutate.estimate('twitter-user', { mutateProperty: 'degree' })
YIELD requiredMemory, bytesMin, bytesMax, heapPercentageMin, heapPercentageMax, nodeCount, relationshipCount;

stima effettiva
CALL gds.degree.mutate('twitter-user', { mutateProperty: 'degree' })
YIELD centralityDistribution, nodePropertiesWritten
RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore, nodePropertiesWritten

CALL gds.graph.nodeProperty.stream('twitter-user', 'degree')
YIELD nodeId, propertyValue
WITH gds.util.asNode(nodeId) AS Id, propertyValue AS scId
MATCH (t:Troll)
WHERE t.name = Id.name AND t.followers_count > 5000
MATCH (u:Troll)
WHERE u.name = Id.name AND u.followers_count > 5000
RETURN t.name as TrollsName, u.name as UsersName

-----------------------------------------------------------
# Seconda query 

Prendo le comunity piu' usate e prendo poi i loro tag maggiori

CALL gds.graph.project('gds-native-twitter', ['User', 'Troll', 'Tweet', 'Hashtag'], '*')
YIELD graphName, nodeCount, relationshipCount;

prima lo faccio vedere senza hashtag

CALL gds.louvain.stream('twitter-user')
YIELD nodeId, communityId
WITH communityId AS communityId, size(collect(nodeId)) as size
WHERE size > 10
RETURN communityId, size
ORDER BY size DESC;

poi con hashtag

CALL gds.louvain.stream('twitter-user', {maxIterations:20})
YIELD nodeId, communityId
WITH communityId AS community, size(collect(nodeId)) as size, 
collect(nodeId) as ids
WHERE size > 10
MATCH (u:User)-->(t)-[*1..2]->(n) 
WHERE id(u) in ids 
AND (t:Tweet)
AND (n:Hashtag OR n:User)
WITH community as community, size as size,  count(t) as count,
CASE WHEN head(labels(n))='Hashtag' THEN '#'+n.tag 
ELSE '@'+n.screen_name END as text
ORDER BY count(t) DESC
RETURN community, size, collect(text)[0..5] AS hashtags_or_users
ORDER BY size DESC

memory stima
CALL gds.louvain.mutate.estimate('gds-native-twitter',
{mutateProperty:'commnuityID'})
YIELD requiredMemory, bytesMin, bytesMax, heapPercentageMin,
heapPercentageMax, nodeCount, relationshipCount;

informazione salvata sul named graph
CALL gds.louvain.mutate('gds-native-twitter', {mutateProperty:'community'})
