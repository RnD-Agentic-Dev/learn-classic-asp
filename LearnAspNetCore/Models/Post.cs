using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace LearnAspNetCore.Models;

[Table("tb_posts")]
public class Post
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    [Column("seq")]
    public int Seq { get; set; }

    [Required(ErrorMessage = "Please write down the title")]
    [Column("title")]
    public string Title { get; set; } = string.Empty;

    [Required(ErrorMessage = "Please write down the content")]
    [Column("content")]
    public string? Content { get; set; }

    [Column("status")]
    public string? Status { get; set; }

    [Column("deleted")]
    [StringLength(10)]
    public string Deleted { get; set; } = "N";
}
