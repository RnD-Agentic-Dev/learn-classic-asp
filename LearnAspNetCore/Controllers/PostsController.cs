using Microsoft.AspNetCore.Mvc;
using LearnAspNetCore.Models;
using LearnAspNetCore.Repositories;

namespace LearnAspNetCore.Controllers;

public class PostsController : Controller
{
    private readonly IPostRepository _postRepository;

    public PostsController(IPostRepository postRepository)
    {
        _postRepository = postRepository;
    }

    [HttpGet]
    public async Task<IActionResult> Create()
    {
        var posts = await _postRepository.GetAllPostsAsync();
        ViewBag.Posts = posts;
        return View(new Post());
    }

    [HttpPost]
    public async Task<IActionResult> Create(Post post)
    {
        string? submit = Request.Form["submit"];
        string? titleMessage = null;
        string? contentMessage = null;
        string? submitMessage = null;

        if (string.IsNullOrEmpty(post.Title) && !string.IsNullOrEmpty(submit))
            titleMessage = "Please write down the title";

        if (string.IsNullOrEmpty(post.Content) && !string.IsNullOrEmpty(submit))
            contentMessage = "Please write down the content";

        if (!string.IsNullOrEmpty(post.Title) && !string.IsNullOrEmpty(post.Content)
            && !string.IsNullOrEmpty(post.Status) && !string.IsNullOrEmpty(submit))
        {
            post.Deleted = "N";
            await _postRepository.CreatePostAsync(post);
            submitMessage = "success submit new post";
            ModelState.Clear();
            post = new Post();
        }

        ViewBag.TitleMessage = titleMessage;
        ViewBag.ContentMessage = contentMessage;
        ViewBag.SubmitMessage = submitMessage;
        ViewBag.Posts = await _postRepository.GetAllPostsAsync();
        return View(post);
    }

    [HttpGet]
    public async Task<IActionResult> Update(int? seq)
    {
        var viewModel = new PostUpdateViewModel
        {
            Posts = await _postRepository.GetActivePostsAsync(),
            DeletedPosts = await _postRepository.GetDeletedPostsAsync()
        };

        if (seq.HasValue)
        {
            viewModel.SelectedPost = await _postRepository.GetPostBySeqAsync(seq.Value);
        }

        return View(viewModel);
    }

    [HttpPost]
    public async Task<IActionResult> Update(int? seq, string submit)
    {
        var viewModel = new PostUpdateViewModel();

        if (submit == "Restore")
        {
            int restoreSeq = int.Parse(Request.Form["seq"]!);
            await _postRepository.RestorePostAsync(restoreSeq);
            viewModel.SubmitMessage = "restore post success";
        }
        else if (submit == "Delete")
        {
            int deleteSeq = int.Parse(Request.Form["seq"]!);
            await _postRepository.SoftDeletePostAsync(deleteSeq);
            viewModel.SubmitMessage = "delete post success";
        }
        else if (submit == "Update")
        {
            string title = Request.Form["title"]!;
            string content = Request.Form["content"]!;
            string status = Request.Form["status"]!;
            int updateSeq = int.Parse(Request.Form["seq"]!);

            if (string.IsNullOrEmpty(title))
                viewModel.TitleMessage = "Please write down the title";

            if (string.IsNullOrEmpty(content))
                viewModel.ContentMessage = "Please write down the content";

            var selectedPost = new Post
            {
                Seq = updateSeq,
                Title = title,
                Content = content,
                Status = status
            };
            viewModel.SelectedPost = selectedPost;

            if (!string.IsNullOrEmpty(title) && !string.IsNullOrEmpty(content) && !string.IsNullOrEmpty(status))
            {
                await _postRepository.UpdatePostAsync(selectedPost);
                viewModel.SubmitMessage = "update post success";
            }
        }

        viewModel.Posts = await _postRepository.GetActivePostsAsync();
        viewModel.DeletedPosts = await _postRepository.GetDeletedPostsAsync();
        return View(viewModel);
    }
}
