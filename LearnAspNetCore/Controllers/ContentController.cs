using Microsoft.AspNetCore.Mvc;

namespace LearnAspNetCore.Controllers;

public class ContentController : Controller
{
    public IActionResult Index()
    {
        ViewBag.Username = "armando";
        ViewBag.Email = "armando@mail.com";
        return View();
    }

    public IActionResult Json()
    {
        var glossary = new
        {
            glossary = new
            {
                title = "example glossary",
                GlossDiv = new
                {
                    title = "S",
                    GlossList = new
                    {
                        GlossEntry = new
                        {
                            ID = "SGML",
                            SortAs = "SGML",
                            GlossTerm = "Standard Generalized Markup Language",
                            Acronym = "SGML",
                            Abbrev = "ISO 8879:1986",
                            GlossDef = new
                            {
                                para = "A meta-markup language, used to create markup languages such as DocBook.",
                                GlossSeeAlso = new[] { "GML", "XML" }
                            },
                            GlossSee = "markup"
                        }
                    }
                }
            }
        };

        return Json(glossary);
    }

    public IActionResult Xml()
    {
        var xml = @"<?xml version=""1.0"" encoding=""UTF-8""?>
<!DOCTYPE glossary PUBLIC ""-//OASIS//DTD DocBook V3.1//EN"" """">
 <glossary><title>example glossary</title>
  <GlossDiv><title>S</title>
   <GlossList>
    <GlossEntry ID=""SGML"" SortAs=""SGML"">
     <GlossTerm>Standard Generalized Markup Language</GlossTerm>
     <Acronym>SGML</Acronym>
     <Abbrev>ISO 8879:1986</Abbrev>
     <GlossDef>
      <para>A meta-markup language, used to create markup
languages such as DocBook.</para>
      <GlossSeeAlso OtherTerm=""GML""/>
      <GlossSeeAlso OtherTerm=""XML""/>
     </GlossDef>
     <GlossSee OtherTerm=""markup""/>
    </GlossEntry>
   </GlossList>
  </GlossDiv>
 </glossary>";

        return Content(xml, "text/xml");
    }

    public IActionResult Redirect()
    {
        return RedirectToAction("Conditional", "Basic");
    }

    public IActionResult Transfer()
    {
        ViewBag.TransferNote = "This demonstrates Server.Transfer - the URL does not change in the browser.";
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

    public IActionResult Execute()
    {
        ViewBag.ExecuteNote = "This demonstrates Server.Execute - the content from another page is included.";
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
}
