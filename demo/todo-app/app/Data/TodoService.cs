namespace TodoWeb.Data;

public class TodoService
{
    private readonly IHttpClientFactory _httpClientFactory;
    private const string BaseUrl = "http://localhost:5000/todos";
    public TodoService(IHttpClientFactory httpClientFactory)
    {
        _httpClientFactory = httpClientFactory;
    }
    
    public async Task<List<Todo>> GetTodosAsync()
    {
        var client = _httpClientFactory.CreateClient();
        var response = await client.GetAsync(BaseUrl);
        var todos = await response.Content.ReadFromJsonAsync<List<Todo>>();
        if (todos == null)
        {
            return new();
        }
        return todos.OrderBy(x=>x.Completed).ThenBy(x=>x.DueDate).ToList();

    }

    public async Task CreateTodoAsync(Todo todo)
    {
        var request = new HttpRequestMessage(HttpMethod.Post, BaseUrl)
        {
            Content = JsonContent.Create(todo)
        };
        await SendAsync(request);
    }

    public async Task UpdateTodoAsync(Todo todo)
    {        
        var request = new HttpRequestMessage(HttpMethod.Put, $"{BaseUrl}/{todo.Id}")
        {
            Content = JsonContent.Create(todo)
        };
        await SendAsync(request);
    }

    public async Task DeleteTodoAsync(int id)
    {
        var request = new HttpRequestMessage(HttpMethod.Delete, $"{BaseUrl}/{id}");
        await SendAsync(request); 
    }

    private async Task SendAsync(HttpRequestMessage request)
    {
        var client = _httpClientFactory.CreateClient();
        var response = await client.SendAsync(request);
        response.EnsureSuccessStatusCode();
    }
}
