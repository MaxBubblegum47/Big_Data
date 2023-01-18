# Prima query 
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
RETURN id(t2) as source, id(t1) as target')

CALL gds.degree.stream('twitter-user')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).screen_name AS name, score 
ORDER BY score DESC LIMIT 10;


CALL gds.degree.mutate('twitter-user', { mutateProperty: 'degree' })
YIELD centralityDistribution, nodePropertiesWritten
RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean 
AS meanScore, nodePropertiesWritten

CALL gds.degree.mutate.estimate('twitter-user', { mutateProperty: 'degree' })
YIELD requiredMemory, bytesMin, bytesMax, 
heapPercentageMin, heapPercentageMax, nodeCount, relationshipCount;

CALL gds.graph.nodeProperty.stream('twitter-user', 'degree')
YIELD nodeId, propertyValue
WITH gds.util.asNode(nodeId) AS Id, propertyValue AS scId
MATCH (t:Troll)
WHERE t.name = Id.name AND t.followers_count > 5000
MATCH (u:Troll)
WHERE u.name = Id.name AND u.followers_count > 5000
RETURN t.name as TrollsName, u.name as UsersNamen

-----------------------------------------------------------
# Seconda query 
CALL gds.graph.project('native-twitter', ['User', 'Troll', 
'Tweet', 'Hashtag'], '*')
YIELD graphName, nodeCount, relationshipCount;

CALL gds.louvain.stream('native-twitter')
YIELD nodeId, communityId
WITH communityId AS communityId, size(collect(nodeId)) as size
WHERE size > 10
RETURN communityId, size
ORDER BY size DESC;

CALL gds.louvain.stream('native-twitter', {maxIterations:10})
YIELD nodeId, communityId
WITH communityId AS community, size(collect(nodeId)) as size, 
collect(nodeId) as ids
WHERE size > 10000
MATCH (u:User)-->(t)-[*1..2]->(n) 
WHERE id(u) in ids 
AND (t:Tweet)
AND (n:Hashtag OR n:User)
WITH community as community, size as size,  count(t) as count,
CASE WHEN head(labels(n))='Hashtag' THEN '#'+n.tag 
ELSE '@'+n.screen_name END as text
ORDER BY count(t) DESC
RETURN community, size, collect(text)[0..5] AS hashtags_or_users
ORDER BY size DESC LIMIT 10;

CALL gds.louvain.mutate.estimate('native-twitter',
{mutateProperty:'commnuityID'})
YIELD requiredMemory, bytesMin, bytesMax, heapPercentageMin,
heapPercentageMax, nodeCount, relationshipCount;

CALL gds.louvain.mutate('gds-native-twitter', {mutateProperty:'community'})
