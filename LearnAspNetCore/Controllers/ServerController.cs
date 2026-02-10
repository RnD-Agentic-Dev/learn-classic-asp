using Microsoft.AspNetCore.Mvc;

namespace LearnAspNetCore.Controllers;

public class ServerController : Controller
{
    public IActionResult Variables()
    {
        var serverVariables = new Dictionary<string, string>();

        foreach (var header in Request.Headers)
        {
            serverVariables[$"HTTP_{header.Key.ToUpper().Replace("-", "_")}"] = header.Value.ToString();
        }

        serverVariables["REQUEST_METHOD"] = Request.Method;
        serverVariables["SERVER_NAME"] = Request.Host.Host;
        serverVariables["SERVER_PORT"] = Request.Host.Port?.ToString() ?? "80";
        serverVariables["SERVER_PROTOCOL"] = Request.Protocol;
        serverVariables["PATH_INFO"] = Request.Path;
        serverVariables["QUERY_STRING"] = Request.QueryString.ToString();
        serverVariables["REMOTE_ADDR"] = HttpContext.Connection.RemoteIpAddress?.ToString() ?? "";
        serverVariables["REMOTE_HOST"] = HttpContext.Connection.RemoteIpAddress?.ToString() ?? "";
        serverVariables["REMOTE_PORT"] = HttpContext.Connection.RemotePort.ToString();
        serverVariables["LOCAL_ADDR"] = HttpContext.Connection.LocalIpAddress?.ToString() ?? "";
        serverVariables["CONTENT_TYPE"] = Request.ContentType ?? "";
        serverVariables["CONTENT_LENGTH"] = Request.ContentLength?.ToString() ?? "0";

        ViewBag.ServerVariables = serverVariables;
        return View();
    }
}
