var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", (IConfiguration config) => $"Hello {config["name"]}!");

app.Run();
