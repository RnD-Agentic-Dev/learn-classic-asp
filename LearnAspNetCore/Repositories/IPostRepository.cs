using LearnAspNetCore.Models;

namespace LearnAspNetCore.Repositories;

public interface IPostRepository
{
    Task<List<Post>> GetAllPostsAsync();
    Task<List<Post>> GetActivePostsAsync();
    Task<List<Post>> GetDeletedPostsAsync();
    Task<Post?> GetPostBySeqAsync(int seq);
    Task CreatePostAsync(Post post);
    Task UpdatePostAsync(Post post);
    Task SoftDeletePostAsync(int seq);
    Task RestorePostAsync(int seq);
}
