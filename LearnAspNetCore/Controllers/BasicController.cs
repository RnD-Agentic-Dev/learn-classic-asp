using Microsoft.AspNetCore.Mvc;

namespace LearnAspNetCore.Controllers;

public class BasicController : Controller
{
    public IActionResult Comment()
    {
        return View();
    }

    public IActionResult Conditional()
    {
        int temperature = 25;
        string message;

        if (temperature < 15)
            message = "<p>Snow will come.</p>";
        else if (temperature >= 15 && temperature < 25)
            message = "<p>Nice weather to have a picnic</p>";
        else if (temperature >= 25 && temperature < 35)
            message = "<p>Summer is coming</p>";
        else
            message = "<p>Woah! It's very hot!</p>";

        ViewBag.Temperature = temperature;
        ViewBag.Message = message;
        return View();
    }

    public IActionResult Loops()
    {
        return View();
    }

    public IActionResult Array()
    {
        string names = "Kim,Mook,Jun,Sung";
        string[] namesSplit = names.Split(',');
        string[] cars = { "Kim", "Mook", "Jun", "Sung" };

        ViewBag.NamesSplit = namesSplit;
        ViewBag.Cars = cars;
        return View();
    }

    public IActionResult Function()
    {
        return View();
    }

    public IActionResult Variable()
    {
        ViewBag.Username = "armando";
        ViewBag.Email = "armando@mail.com";
        return View();
    }
}
