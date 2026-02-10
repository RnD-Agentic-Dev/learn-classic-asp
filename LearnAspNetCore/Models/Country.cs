using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace LearnAspNetCore.Models;

[Table("tb_countries")]
public class Country
{
    [Column("seq")]
    public int? Seq { get; set; }

    [Column("name")]
    public string Name { get; set; } = string.Empty;

    [Column("code")]
    public string? Code { get; set; }

    [Column("currency")]
    public string? Currency { get; set; }

    [Column("population")]
    public string? Population { get; set; }

    [Column("capital")]
    public string? Capital { get; set; }
}
