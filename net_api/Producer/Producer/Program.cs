var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddCap(x =>
{
    x.UseRabbitMQ(opt=>
    {
        opt.HostName = "localhost";
        opt.Port = 5672;
        opt.Password = "rabbitmqpassword";
        opt.UserName = "rabbitmquser";
        opt.ExchangeName = "fastapi";
    });
    
    x.UseInMemoryStorage();
    x.UseDashboard();
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();