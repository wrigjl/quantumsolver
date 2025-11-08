
//
// This program tests the Deutsch solver endpoint by sending various problems
// via json and parsing the resulting json to verify the answer.
//
// It sure is longer and uglier than the python version.
//

using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.CommandLine;

class Program
{
    static void Main(string[] args)
    {
        RootCommand rootCommand = new("Deutsch Endpoint Tester") {
            new Option<string>("--baseurl")
            {
                Description = "The endpoint base url.",
                DefaultValueFactory = (x) => "http://127.0.0.1:5001",
            },
            new Option<string>("--endpoint")
            {
                Description = "The endpoint name.",
                DefaultValueFactory = (x) => "deutsch-classical",
            },
        };
        rootCommand.SetAction(parseResult =>   
        {
            var baseurl = parseResult.GetValue<string>("--baseurl");
            var endpoint = parseResult.GetValue<string>("--endpoint");
            Console.WriteLine($"Testing endpoint {baseurl}/{endpoint}");
            TryIt($"{baseurl}/{endpoint}", new Boolean[] { true, true }, "constant");
            TryIt($"{baseurl}/{endpoint}", new Boolean[] { false, false }, "constant");
            TryIt($"{baseurl}/{endpoint}", new Boolean[] { true, false }, "balanced");
            TryIt($"{baseurl}/{endpoint}", new Boolean[] { false, true }, "balanced");
            Console.WriteLine("All tests passed.");
        });

        ParseResult parseResult = rootCommand.Parse(args);
        parseResult.Invoke();
    }

    static void TryIt(string url, Boolean[] problem, string expected)
    {
        using HttpClient client = new();
        client.DefaultRequestHeaders.Accept.Clear();
        var json = JsonSerializer.Serialize(problem);
        var content = new StringContent(json.ToString(), Encoding.UTF8, "application/json");
        var response = client.PostAsync(url, content).GetAwaiter().GetResult();
        var respStream = new StreamReader(response.Content.ReadAsStream());
        var responseBody = respStream.ReadToEnd();

        JsonObject result = JsonNode.Parse(responseBody)!.AsObject();

        if (!result.TryGetPropertyValue("answer", out JsonNode? answerNode) || answerNode == null)
        {
            throw new ArgumentException($"Error: response does not contain 'answer' for problem {string.Join(",", problem)}");
        }

        var answerText = answerNode.ToString();
        if (answerText != expected)
        {
            throw new ArgumentException($"Error: expected {expected}, got {answerText} for problem {string.Join(",", problem)}");
        }
    }
}
