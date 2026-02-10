using Microsoft.AspNetCore.Mvc;
using LearnAspNetCore.Models;

namespace LearnAspNetCore.Controllers;

public class FormsController : Controller
{
    public IActionResult Get()
    {
        var model = new FormViewModel
        {
            Title = Request.Query["title"],
            Content = Request.Query["content"],
            Category = Request.Query["category"],
            Status = Request.Query["status"]
        };
        return View(model);
    }

    public IActionResult GetValidation()
    {
        var model = new FormViewModel
        {
            Title = Request.Query["title"],
            Content = Request.Query["content"],
            Category = Request.Query["category"],
            Status = Request.Query["status"],
            Submit = Request.Query["submit"]
        };

        if (string.IsNullOrEmpty(model.Title) && !string.IsNullOrEmpty(model.Submit))
            model.TitleMessage = "Please write down the title";

        if (string.IsNullOrEmpty(model.Content) && !string.IsNullOrEmpty(model.Submit))
            model.ContentMessage = "Please write down the content";

        return View(model);
    }

    [HttpGet]
    public IActionResult Post()
    {
        return View(new FormViewModel());
    }

    [HttpPost]
    public IActionResult Post(FormViewModel model)
    {
        return View(model);
    }

    [HttpGet]
    public IActionResult PostValidation()
    {
        return View(new FormViewModel());
    }

    [HttpPost]
    public IActionResult PostValidation(FormViewModel model)
    {
        model.Submit = Request.Form["submit"];

        if (string.IsNullOrEmpty(model.Title) && !string.IsNullOrEmpty(model.Submit))
            model.TitleMessage = "Please write down the title";

        if (string.IsNullOrEmpty(model.Content) && !string.IsNullOrEmpty(model.Submit))
            model.ContentMessage = "Please write down the content";

        return View(model);
    }
}
