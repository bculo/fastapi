using System.Runtime.Serialization.Json;
using System.Text;
using DotNetCore.CAP;
using Microsoft.AspNetCore.Mvc;
using RabbitMQ.Client;

namespace Producer.Controllers;

[ApiController]
[Route("[controller]")]
public class PublisherController : ControllerBase
{
    [HttpPost]
    public async Task<IActionResult> CreateOrder([FromBody] MessageDto request)
    {
        ICapPublisher publisher = null;
        ConnectionFactory factory = new ConnectionFactory();
        factory.UserName = "rabbitmquser";
        factory.Password = "rabbitmqpassword";
        factory.HostName = "localhost";
        factory.Port = 5672;

        IConnection connection = factory.CreateConnection();
        IModel channel = connection.CreateModel();
        
        IDictionary<string, object> headers = new Dictionary<string, object>();
        headers.Add("task", "celery_instance.send_push_notification");
        headers.Add("id", Guid.NewGuid().ToString());

        IBasicProperties props = channel.CreateBasicProperties();
        props.Headers = headers;
        props.CorrelationId = (string)headers["id"];
        props.ContentEncoding = "utf-8";
        props.ContentType = "application/json";

        object[] taskArgs = { request.Text };
        object[] arguments = { taskArgs, new(), new() };

        using var stream = new MemoryStream();
        var ser = new DataContractJsonSerializer(typeof(object[]));
        ser.WriteObject(stream, arguments);
        stream.Position = 0;
        using var sr = new StreamReader(stream);
        var message = await sr.ReadToEndAsync();
        
        var body = Encoding.UTF8.GetBytes(message);
        
        channel.BasicPublish(exchange: "fastapi",
            routingKey: "fastapi",
            basicProperties: props,
            body: body);
        
        return NoContent();
    }
}

public class MessageDto
{
    public string Text { get; set; }
}