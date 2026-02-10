using Microsoft.AspNetCore.Mvc;

namespace LearnAspNetCore.Controllers;

public class FileSystemController : Controller
{
    private readonly IWebHostEnvironment _env;

    public FileSystemController(IWebHostEnvironment env)
    {
        _env = env;
    }

    public IActionResult List()
    {
        var drives = DriveInfo.GetDrives();
        var driveLetters = drives.Select(d => d.Name).ToList();

        string folderPath = _env.ContentRootPath;
        var folderInfo = new DirectoryInfo(folderPath);

        string filePath = Path.Combine(_env.ContentRootPath, "Program.cs");
        var fileInfo = new FileInfo(filePath);

        ViewBag.DriveLetters = driveLetters;
        ViewBag.FolderPath = folderPath;
        ViewBag.FolderSize = folderInfo.EnumerateFiles("*", SearchOption.AllDirectories).Sum(f => f.Length);
        ViewBag.FolderCreated = folderInfo.CreationTime;
        ViewBag.FilePath = filePath;
        ViewBag.FileSize = fileInfo.Length;
        ViewBag.FileCreated = fileInfo.CreationTime;

        return View();
    }

    public IActionResult ReadFile()
    {
        string filePath = Path.Combine(_env.ContentRootPath, "files", "countries.txt");
        var lines = new List<string[]>();

        if (System.IO.File.Exists(filePath))
        {
            foreach (var line in System.IO.File.ReadLines(filePath))
            {
                if (!string.IsNullOrWhiteSpace(line))
                {
                    lines.Add(line.Split(','));
                }
            }
        }

        ViewBag.FileName = "files/countries.txt";
        ViewBag.Lines = lines;
        return View();
    }

    public IActionResult WriteFile()
    {
        string filePath = Path.Combine(_env.ContentRootPath, "files", "cities.txt");

        string content = "This is my first sentence. And then second sentence.\n";
        content += "written at " + DateTime.Now + "\n";

        System.IO.File.WriteAllText(filePath, content);

        ViewBag.FileName = "files/cities.txt";
        ViewBag.Message = "File written successfully";
        return View();
    }

    public IActionResult WriteFileAppend()
    {
        string filePath = Path.Combine(_env.ContentRootPath, "files", "cities.txt");

        string content = "This is my updated sentence.\n";
        content += "written at " + DateTime.Now + "\n";

        System.IO.File.AppendAllText(filePath, content);

        ViewBag.FileName = "files/cities.txt";
        ViewBag.Message = "File appended successfully";
        return View();
    }
}
