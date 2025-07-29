package main 

import (
	"fmt"
	"time"
	"math/rand"
	"math"
)

func main() {
	fmt.Println("Hello world!")

	fmt.Println("The time is", time.Now())

	fmt.Println("My favorite number is", rand.Intn(10))

	fmt.Printf("%g problems. \n", math.Sqrt(7))
}
