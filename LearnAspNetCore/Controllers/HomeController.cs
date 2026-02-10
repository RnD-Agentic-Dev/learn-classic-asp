using Microsoft.AspNetCore.Mvc;

namespace LearnAspNetCore.Controllers;

public class HomeController : Controller
{
    public IActionResult Index()
    {
        return View();
    }
}
