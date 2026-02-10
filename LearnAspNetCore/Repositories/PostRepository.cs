using Microsoft.EntityFrameworkCore;
using LearnAspNetCore.Data;
using LearnAspNetCore.Models;

namespace LearnAspNetCore.Repositories;

public class PostRepository : IPostRepository
{
    private readonly ApplicationDbContext _context;

    public PostRepository(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<List<Post>> GetAllPostsAsync()
    {
        return await _context.Posts.ToListAsync();
    }

    public async Task<List<Post>> GetActivePostsAsync()
    {
        return await _context.Posts.Where(p => p.Deleted == "N").ToListAsync();
    }

    public async Task<List<Post>> GetDeletedPostsAsync()
    {
        return await _context.Posts.Where(p => p.Deleted == "Y").ToListAsync();
    }

    public async Task<Post?> GetPostBySeqAsync(int seq)
    {
        return await _context.Posts.FirstOrDefaultAsync(p => p.Seq == seq);
    }

    public async Task CreatePostAsync(Post post)
    {
        post.Deleted = "N";
        _context.Posts.Add(post);
        await _context.SaveChangesAsync();
    }

    public async Task UpdatePostAsync(Post post)
    {
        var existing = await _context.Posts.FirstOrDefaultAsync(p => p.Seq == post.Seq);
        if (existing != null)
        {
            existing.Title = post.Title;
            existing.Content = post.Content;
            existing.Status = post.Status;
            await _context.SaveChangesAsync();
        }
    }

    public async Task SoftDeletePostAsync(int seq)
    {
        var post = await _context.Posts.FirstOrDefaultAsync(p => p.Seq == seq);
        if (post != null)
        {
            post.Deleted = "Y";
            await _context.SaveChangesAsync();
        }
    }

    public async Task RestorePostAsync(int seq)
    {
        var post = await _context.Posts.FirstOrDefaultAsync(p => p.Seq == seq);
        if (post != null)
        {
            post.Deleted = "N";
            await _context.SaveChangesAsync();
        }
    }
}
