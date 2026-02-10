using Microsoft.AspNetCore.Mvc;
using LearnAspNetCore.Models;

namespace LearnAspNetCore.Controllers;

public class AccountController : Controller
{
    [HttpGet]
    public IActionResult SessionSimple()
    {
        var currentUser = HttpContext.Session.GetString("currentUser") ?? "";
        ViewBag.CurrentUser = currentUser;
        return View();
    }

    [HttpPost]
    public IActionResult SessionSimple(string submit)
    {
        if (submit == "Logout")
        {
            HttpContext.Session.SetString("currentUser", "");
        }
        else if (submit == "Login")
        {
            HttpContext.Session.SetString("currentUser", "Park Kwang Hoo!");
        }

        ViewBag.CurrentUser = HttpContext.Session.GetString("currentUser") ?? "";
        return View();
    }

    [HttpGet]
    public IActionResult Login()
    {
        var model = new LoginViewModel
        {
            CurrentUser = HttpContext.Session.GetString("currentUser") ?? "",
            IsLoggedIn = !string.IsNullOrEmpty(HttpContext.Session.GetString("currentUser"))
        };
        return View(model);
    }

    [HttpPost]
    public IActionResult Login(string? username, string? password, string submit)
    {
        string message = "";

        if (submit == "Logout")
        {
            HttpContext.Session.SetString("currentUser", "");
        }
        else if (submit == "Login")
        {
            if (string.IsNullOrEmpty(username))
                message += "username is required <br/>";

            if (string.IsNullOrEmpty(password))
                message += "password is required <br/>";

            if (!string.IsNullOrEmpty(username) && !string.IsNullOrEmpty(password))
            {
                if (username != "user" || password != "user")
                {
                    message += "username or password is wrong";
                }
                else
                {
                    HttpContext.Session.SetString("currentUser", username);
                }
            }
        }

        var model = new LoginViewModel
        {
            Message = message,
            CurrentUser = HttpContext.Session.GetString("currentUser") ?? "",
            IsLoggedIn = !string.IsNullOrEmpty(HttpContext.Session.GetString("currentUser"))
        };
        return View(model);
    }
}
