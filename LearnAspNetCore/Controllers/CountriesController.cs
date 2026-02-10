using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using LearnAspNetCore.Data;

namespace LearnAspNetCore.Controllers;

public class CountriesController : Controller
{
    private readonly ApplicationDbContext _context;

    public CountriesController(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<IActionResult> Index()
    {
        var countries = await _context.Countries.ToListAsync();
        return View(countries);
    }
}
