exports.handler = async (event) => {
    var AWS = require('aws-sdk');
    
    AWS.config.update({region: 'us-east-1'});

    var lexruntime = new AWS.LexRuntime();
    
    const response = {
            statusCode: 200,
            headers: {
                "Access-Control-Allow-Headers" : "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                messages: [{
                    type: 'unstructured',
                    unstructured: {
                        text:'Some error occurred. Please come back later.'
                    }
                }]
            })
        };
    
    console.log("Event", JSON.stringify(event));
    const message = JSON.parse(event.body).messages[0].unstructured.text;
    const userId = event.requestContext.accountId;
    console.log("The message is", message);
    try {

    	var params = {
        	botAlias: '$LATEST', /* required, has to be '$LATEST' */
        	botName: 'YelpRestaurantRecommender', /* required, the name of you bot */
        	inputText: message, /* required, your text */
        	userId: userId, /* required, arbitrary identifier */
        	sessionAttributes: {
        	    someKey: 'STRING_VALUE',
    	    }
	    };

    return lexruntime.postText(params).promise()
            .then((data) =>{
                console.log('response successful', data, message);
                const response = {
                                statusCode: 200,
                                headers: {
                                    "Access-Control-Allow-Headers" : "*",
                                    "Access-Control-Allow-Origin": "*",
                                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                                    "Content-Type": "application/json"
                                },
                                body: JSON.stringify({
                                    messages: [{
                                        type: 'unstructured',
                                        unstructured: {
                                            text: data.message
                                                      }
                                                }]
                                })
                                };
            return response;
            })
            .catch((err) =>{
                console.log(err);
            });
	} catch (err) {
	    console.log("The error is ", err);
	    return response;
	}

  
};
