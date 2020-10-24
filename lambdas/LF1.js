

exports.handler = async (event) => {
    // TODO implement
    if(!event) {
        const response = {
                "dialogAction":{
                    "fulfillmentState":"Fulfilled",
                    "type":"Close",
                    "message":{
                        "contentType":"PlainText",
                        "content": "Some error occurred"
                    }
                }
            }
            return response;
    }
    const eventName = event.currentIntent.name;
    if(event.invocationSource === "FulfillmentCodeHook" && eventName === "DiningSuggestionsIntent") {
        var sqsQueueUrl = "https://sqs.us-east-1.amazonaws.com/092590414170/Yelp-Bot";
        var AWS = require('aws-sdk');
        AWS.config.update({region: 'us-east-1'});
        var sqs = new AWS.SQS();
        
        console.log(JSON.stringify(event) + eventName)
        
        var params = {
            DelaySeconds: 10,
            MessageAttributes: {
              "Location": {
                DataType: "String",
                StringValue: event.currentIntent.slots.Location
              },
              "Cuisine": {
                DataType: "String",
                StringValue: event.currentIntent.slots.Cuisine
              },
              "Time": {
                DataType: "String",
                StringValue: event.currentIntent.slots.Time
              },
              "Phone": {
                DataType: "String",
                StringValue:  event.currentIntent.slots.Phone
              },
              "Number": {
                DataType: "String",
                StringValue:  event.currentIntent.slots.Number
              }
            },
            MessageBody: JSON.stringify(event),
            QueueUrl: sqsQueueUrl
        };

        try{
            await sqs.sendMessage(params).promise();
            console.log("Success");
            const response = {
                                "dialogAction":{
                                    "fulfillmentState":"Fulfilled",
                                    "type":"Close",
                                    "message":{
                                        "contentType":"PlainText",
                                        "content": "Thanks for the information. I will send you the restaurant recommendations shortly through an SMS! Have a good day"
                                    }
                                }
                            }
            return response;
            
            }
        catch(err){
            console.log(err);
        }
    }
    
    //  return sqs.sendMessage(params).promise()
    //     .then((data) => {
    //         console.log("Success");
    //         const response = {
    //             "dialogAction":{
    //                 "fulfillmentState":"Fulfilled",
    //                 "type":"Close",
    //                 "message":{
    //                     "contentType":"PlainText",
    //                     "content": "Thanks for the information. I will send you the restaurant recommendations shortly through an SMS! Have a good day"
    //                 }
    //             }
    //         }
    //         return response;
    //     }).catch((err) => {
    //         console.log(err);
    //     })
    // }
 
};
