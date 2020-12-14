# Restaurant Recommendation Microservice

Restaurant Recommendation Bot microservice uses scraped restaurants from Yelp for particular cuisine types to build a database of top restaurants in a given location. The search uses Elastic Search based on cuisine type. The suggestions are sent to the user's phone number via SMS which uses SNS and SQS for gauranteed delivery. 

### Architecture Diagram 

![alt text](https://github.com/rishiraj824/Restaurant-Recommendation-Bot/blob/main/image.png)
