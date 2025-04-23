package main

import (
	"crypto/sha256"
	"fmt"
	"github.com/dgrijalva/jwt-go"
	"github.com/gin-gonic/gin"
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/postgres"
	"github.com/joho/godotenv"
	"golang.org/x/crypto/bcrypt"
	"log"
	"os"
	"time"
)

var db *gorm.DB
var secretKey = []byte("mySecretKey")

type User struct {
	ID        uint   `json:"id"`
	FirstName string `json:"first_name"`
	LastName  string `json:"last_name"`
	Age       int    `json:"age"`
	Email     string `json:"email"`
	Sex       string `json:"sex"`
	Password  string `json:"password" gorm:"-"`
}

type Credential struct {
	UserID       uint   `json:"user_id"`
	PasswordHash string `json:"password_hash"`
}

type Token struct {
	UserID     uint      `json:"user_id"`
	TokenHash  string    `json:"token_hash"`
	ExpiryDate time.Time `json:"expiry_date"`
	Revoked    bool      `json:"revoked"`
}

func register(c *gin.Context) {
	var user User
	var credential Credential
	err := c.ShouldBindJSON(&user)
	if err != nil {
		c.JSON(400, gin.H{"error": err.Error()})
		return
	}

	passwordHash, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)
	if err != nil {
		c.JSON(500, gin.H{"error": "Failed to hash password"})
		return
	}

	tx := db.Begin()
	defer func() {
		if r := recover(); r != nil {
			tx.Rollback()
		}
	}()
	err = db.Create(&user).Error
	if err != nil {
		fmt.Println(err.Error())
		c.JSON(500, gin.H{"error": "Failed to register user"})
		return
	}

	credential = Credential{
		UserID:       user.ID,
		PasswordHash: string(passwordHash),
	}

	if err := db.Create(&credential).Error; err != nil {
		c.JSON(500, gin.H{"error": "Failed to store credentials"})
		return
	}

	c.JSON(200, gin.H{"message": "User registered successfully"})
}

func login(c *gin.Context) {
	var user User
	var credential Credential
	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(400, gin.H{"error": err.Error()})
		return
	}

	if err := db.Where("email = ?", user.Email).First(&user).Error; err != nil {
		c.JSON(404, gin.H{"error": "User not found"})
		return
	}

	if err := db.Where("user_id = ?", user.ID).First(&credential).Error; err != nil {
		c.JSON(404, gin.H{"error": "Credentials not found"})
		return
	}

	if err := bcrypt.CompareHashAndPassword([]byte(credential.PasswordHash), []byte(user.Password)); err != nil {
		c.JSON(401, gin.H{"error": "Invalid credentials"})
		return
	}

	claims := jwt.MapClaims{
		"user_id": user.ID,
		"exp":     time.Now().Add(time.Hour * 24).Unix(),
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString(secretKey)
	if err != nil {
		c.JSON(500, gin.H{"error": "Failed to generate token"})
		return
	}

	tokenHash := sha256.Sum256([]byte(tokenString))
	tokenEntry := Token{
		UserID:     user.ID,
		TokenHash:  fmt.Sprintf("%x", tokenHash),
		ExpiryDate: time.Now().Add(time.Hour * 24),
	}
	err = db.Create(&tokenEntry).Error
	if err != nil {
		c.JSON(500, gin.H{"error": "Failed to store refresh token"})
		return
	}

	c.JSON(200, gin.H{"access_token": tokenString})
}

func authMiddleware(c *gin.Context) {
	tokenString := c.GetHeader("Authorization")
	if tokenString == "" {
		c.JSON(401, gin.H{"error": "Authorization token is required"})
		c.Abort()
		return
	}

	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		return secretKey, nil
	})

	if err != nil || !token.Valid {
		c.JSON(401, gin.H{"error": "Invalid or expired token"})
		c.Abort()
		return
	}

	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok {
		c.JSON(401, gin.H{"error": "Invalid claims"})
		c.Abort()
		return
	}

	c.Set("user_id", claims["user_id"])
	c.Next()
}
func main() {
	var err error
	err = godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	dbUser := os.Getenv("DB_USER")
	dbPassword := os.Getenv("DB_PASSWORD")
	dbName := os.Getenv("DB_NAME")
	dsn := fmt.Sprintf("host=postgres	 port=5432 user=%s "+
		"dbname=%s password=%s sslmode=disable search_path=auth", dbUser, dbName, dbPassword)
	fmt.Println(dsn)
	db, err = gorm.Open("postgres", dsn)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	r := gin.Default()

	r.POST("/register", register)
	r.POST("/login", login)

	r.GET("/profile", authMiddleware, func(c *gin.Context) {
		userID := c.MustGet("user_id")
		c.JSON(200, gin.H{"message": fmt.Sprintf("Welcome, user %v", userID)})
	})

	r.Run(":8080")
}
