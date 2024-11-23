using Microsoft.AspNetCore.Mvc;
using System.Linq;
using System.Collections.Generic;

namespace MyApiProject.Controllers
{
    [ApiController]
    [Route("api/cars")]
    public class CarsController : ControllerBase
    {
        private static List<Car> Cars = new List<Car>
        {
            new Car { Id = 711, Model = "Model S", Brand = "Tesla", Color = "Red" },
            new Car { Id = 712, Model = "Corolla", Brand = "Toyota", Color = "Blue" },
            new Car { Id = 713, Model = "Civic", Brand = "Honda", Color = "Black" }
        };

        private static List<Driver> Drivers = new List<Driver>
        {
            new Driver { Id = 1, Name = "John Doe", CarId = 711 },
            new Driver { Id = 2, Name = "Jane Smith", CarId = 711 },
            new Driver { Id = 3, Name = "Mike Brown", CarId = 712 }
        };

        [HttpGet]
        public IActionResult GetAllCars([FromQuery] string color, [FromQuery] string model, [FromQuery] int? offset, [FromQuery] int? limit, [FromQuery] string sort)
        {
            var cars = Cars.AsQueryable();

            if (!string.IsNullOrEmpty(color))
            {
                cars = cars.Where(c => c.Color.ToLower() == color.ToLower());
            }

            if (!string.IsNullOrEmpty(model))
            {
                cars = cars.Where(c => c.Model.ToLower().Contains(model.ToLower()));
            }

            if (!string.IsNullOrEmpty(sort))
            {
                var sortParams = sort.Split(',');
                foreach (var param in sortParams)
                {
                    if (param.StartsWith("-"))
                    {
                        var field = param.Substring(1);
                        cars = cars.OrderByDescending(c => GetPropertyValue(c, field));
                    }
                    else
                    {
                        cars = cars.OrderBy(c => GetPropertyValue(c, param));
                    }
                }
            }

            if (offset.HasValue && limit.HasValue)
            {
                cars = cars.Skip(offset.Value).Take(limit.Value);
            }

            return Ok(cars.ToList());
        }
        [HttpGet("{carId}")]
        public IActionResult GetCarById(int carId)
        {
            var car = Cars.FirstOrDefault(c => c.Id == carId);
            if (car == null) return NotFound();
            return Ok(car);
        }

        [HttpGet("{carId}/drivers")]
        public IActionResult GetDriversByCarId(int carId)
        {
            var drivers = Drivers.Where(d => d.CarId == carId).ToList();
            return Ok(drivers);
        }

        [HttpPost]
        public IActionResult CreateCar([FromBody] Car newCar)
        {
            if (newCar == null)
            {
                return BadRequest("Invalid data.");
            }
            Cars.Add(newCar);
            return CreatedAtAction(nameof(GetCarById), new { carId = newCar.Id }, newCar);
        }

        [HttpPut("{carId}")]
        public IActionResult UpdateCar(int carId, [FromBody] Car updatedCar)
        {
            if (updatedCar == null)
            {
                return BadRequest("Invalid data.");
            }

            var car = Cars.FirstOrDefault(c => c.Id == carId);
            if (car == null)
            {
                return NotFound();
            }

            car.Model = updatedCar.Model;
            car.Brand = updatedCar.Brand;
            car.Color = updatedCar.Color;

            return Ok(car);
        }

        private object GetPropertyValue(Car car, string propertyName)
        {
            var property = typeof(Car).GetProperty(propertyName);
            return property?.GetValue(car, null);
        }
    }
}
