Reference https://docs.microsoft.com/en-us/azure/cognitive-services/anomaly-detector/quickstarts/client-libraries?tabs=windows&pivots=programming-language-csharp

# Quickstart: Use the Incident Detector client library
16/09/2021, 23 minutes to read

Get started with the Incident Detector client library for Python.
Follow these steps to install the package and start using the algorithms provided by logsight.ai service.
The Incident Detector service enables you to find incidents in your logs 
by automatically using deep learning models trained on millions lines of code, regardless of the underlying IT system, failure scenario, or data volume.

Use the Incident Detector client library for Python to:

+ Send data logs to your account workspace (???) 
+ Detect incidents throughout your data logs, as a batch request (???)
+ Detect the incident status of the latest data point in your time series
+ Detect (???) trend change points in your data set.

## Prerequisites
+ Logsight.ai subscription (create one for free to get your private key)
+ Once you have your subscription, create an App resource in the portal.
+ You will need the key to connect your App to the Incident Detector API.
+ You'll paste your key into the code below later in the quickstart.

## Setting up

### Create an environment variable

Using the key from your subscription, create one environment variables for authentication:

+ `INCIDENT_DETECTOR_KEY` - The resource key for authenticating your requests.

Copy the following text to your bash file:

```console
export INCIDENT_DETECTOR_KEY=<replace-with-your-anomaly-detector-key>
```

After you add the environment variable, run source ~/.bashrc from your console window to make the changes effective.


### Install the client library

Within the application directory, 
install the Incident Detector client library for python with the following command:

```console
dotnet add package Microsoft.Azure.CognitiveServices.AnomalyDetector
```

In the application's main() method, create variables for your resource's Azure location,
and your key as an environment variable. 
If you created the environment variable after application is launched,
the editor, IDE, or shell running it will need to be closed and reloaded to access the variable.

```python
static void Main(string[] args){
    //This sample assumes you have created an environment variable for your key and endpoint
    string endpoint = Environment.GetEnvironmentVariable("ANOMALY_DETECTOR_ENDPOINT");
    string key = Environment.GetEnvironmentVariable("ANOMALY_DETECTOR_KEY");
    string datapath = "request-data.csv";

    IAnomalyDetectorClient client = createClient(endpoint, key); //Anomaly Detector client

    Request request = GetSeriesFromFile(datapath); // The request payload with points from the data file

    EntireDetectSampleAsync(client, request).Wait(); // Async method for batch anomaly detection
    LastDetectSampleAsync(client, request).Wait(); // Async method for analyzing the latest data point in the set
    DetectChangePoint(client, request).Wait(); // Async method for change point detection

    Console.WriteLine("\nPress ENTER to exit.");
    Console.ReadLine();
} 
```


## Object model
aaa


## Code examples

Code snippets show you how to do the following with the Incident Detector client library for Python:

+ Authenticate the client
+ Load log data from a file
+ Detect incident in the entire data set
+ Detect the anomaly status of the latest data point (???)
+ Detect the change points in the data set (???)


### Authenticate the client

In a new method, instantiate a client with your endpoint and key.
Create an ApiKeyServiceClientCredentials object with your key,
and use it with your endpoint to create an AnomalyDetectorClient object.


```python
static IAnomalyDetectorClient createClient(string endpoint, string key)
{
    IAnomalyDetectorClient client = new AnomalyDetectorClient(new ApiKeyServiceClientCredentials(key))
    {
        Endpoint = endpoint
    };
    return client;
}
```

### Load log data from a file


### Detect incident in the entire data set


### Detect the anomaly status of the latest data point (???)


### Detect the change points in the data set (???)


## Run the application

Run the application with the dotnet run command from your application directory.

```console
dotnet run
```

## Clean up resources

If you want to clean up and remove a Cognitive Services subscription,
you can delete the resource or resource group.
Deleting the resource group also deletes any other resources associated with the resource group.