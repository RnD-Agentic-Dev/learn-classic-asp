using Microsoft.EntityFrameworkCore;
using LearnAspNetCore.Models;

namespace LearnAspNetCore.Data;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options)
    {
    }

    public DbSet<Post> Posts { get; set; }
    public DbSet<Country> Countries { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Post>(entity =>
        {
            entity.ToTable("tb_posts");
            entity.HasKey(e => e.Seq);
            entity.Property(e => e.Seq).UseIdentityAlwaysColumn();
        });

        modelBuilder.Entity<Country>(entity =>
        {
            entity.ToTable("tb_countries");
            entity.HasNoKey();
        });
    }
}
