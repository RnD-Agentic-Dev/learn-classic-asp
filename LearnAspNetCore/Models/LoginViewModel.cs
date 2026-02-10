namespace LearnAspNetCore.Models;

public class LoginViewModel
{
    public string? Username { get; set; }
    public string? Password { get; set; }
    public string? Message { get; set; }
    public bool IsLoggedIn { get; set; }
    public string? CurrentUser { get; set; }
}
