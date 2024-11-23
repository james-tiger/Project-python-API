public class Car
{
    public int Id { get; set; }
    public string Model { get; set; }
    public string Brand { get; set; }
    public string Color { get; set; }
}

public class Driver
{
    public int Id { get; set; }
    public string Name { get; set; }
    public int CarId { get; set; }
}
