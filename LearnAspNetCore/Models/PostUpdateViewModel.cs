namespace LearnAspNetCore.Models;

public class PostUpdateViewModel
{
    public Post? SelectedPost { get; set; }
    public List<Post> Posts { get; set; } = new();
    public List<Post> DeletedPosts { get; set; } = new();
    public string? TitleMessage { get; set; }
    public string? ContentMessage { get; set; }
    public string? SubmitMessage { get; set; }
    public string[] StatusOptions { get; set; } = new[] { "published", "draft" };
}
