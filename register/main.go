package main

import (
	"bytes"
	"database/sql"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/smtp"
	"strings"

	//  "github.com/gorilla/handlers"
	//	"github.com/gorilla/handlers"
	//	"github.com/gorilla/mux"

	_ "github.com/lib/pq"
)

// const (
// 	host     = "localhost"
// 	port     = 5432
// 	user     = "meet"
// 	password = "meet"
// 	dbname   = "meet"
// )

type Response struct {
	Msg  string `json:"msg"`
	Dbid string `json:"dbid"`
}

func sendConfirmationEmail(email string, dbid int) {
	from := "ma91721@gmail.com"
	password := "ovnekwarguxmkyto"

	to := []string{email}

	smtpHost := "smtp.gmail.com"
	smtpPort := "587"

	mail := fmt.Sprintf("Paste the below link to verify your email address\nlocalhost:8101/api/register/accept/%d", dbid)
	message := []byte(mail)

	auth := smtp.PlainAuth("", from, password, smtpHost)
  fmt.Print("Okk")
	err := smtp.SendMail(smtpHost+":"+smtpPort, auth, from, to, message)
  fmt.Print("Reache")
	if err != nil {
		fmt.Println(err)
		return
	}
}

func sendConfirmation(w http.ResponseWriter, r *http.Request) {
	fmt.Print("SD")
	fmt.Println(r.Method)

	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	if r.Method == "POST" {
		body, _ := io.ReadAll(r.Body)
		keyVal := make(map[string]string)
		json.Unmarshal(body, &keyVal)
		fname := keyVal["fname"]
		lname := keyVal["lname"]
		email := keyVal["email"]
		password := keyVal["password"]

		fmt.Printf("\n%d\n%s\n%s\n%s", len(fname), lname, email, password)
		connStr := "postgres://postgres:password@localhost/postgres?sslmode=disable"
		db, err := sql.Open("postgres", connStr)

		if err != nil {
			panic(err)
		}
		err = db.Ping()
		if err != nil {
			panic(err)
		}

		insertQuery := `INSERT INTO "userdata" ("fname", "lname", "email", "password") VALUES ($1, $2, $3, $4)`
		_, err = db.Exec(insertQuery, fname, lname, email, password)
		//    fmt.Print("Reached here==========================================================================\n");
		if err != nil {
			responseMsg := Response{Msg: "Email address already exists", Dbid: "-1"}
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusNotAcceptable)
			json.NewEncoder(w).Encode(responseMsg)

		} else {
			dbQuery := `SELECT dbid FROM "userdata" WHERE email = $1`
			rows, _ := db.Query(dbQuery, email)
			// if err != nil {
			//      fmt.Print("Hehehe lagi gaya======================================");
			// }
			for rows.Next() {
				var dbid int
				err = rows.Scan(&dbid)
				if err != nil {
					panic(err)
				}
				sendConfirmationEmail(email, dbid)
			}
			responseMsg := Response{Msg: "Please verify your email address", Dbid: "1"}
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusOK)
			json.NewEncoder(w).Encode(responseMsg)
		}
	} else {
		responseMsg := Response{Msg: "Method not allowed", Dbid: "-1"}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusMethodNotAllowed)
		json.NewEncoder(w).Encode(responseMsg)
	}
}
func processConfirmation(w http.ResponseWriter, r *http.Request) {
	fmt.Println(r.Method)

	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	url := strings.Split(r.URL.Path[1:], "/")

	dbid := url[len(url)-1]

	if r.Method == "GET" {
		connStr := "postgres://postgres:password@localhost/postgres?sslmode=disable"
		db, err := sql.Open("postgres", connStr)

		if err != nil {
			panic(err)
		}
		err = db.Ping()
		if err != nil {
			panic(err)
		}

		queryString := `select isverified from userdata where dbid=$1`
		row, _ := db.Query(queryString, dbid)
		for row.Next() {
			var isverified string
			_ = row.Scan(&isverified)
			if isverified == "false" {
				// adding to mongo database
				jsonBody := []byte(fmt.Sprintf(`{"dbid": "%s"}`, dbid))
				bodyReader := bytes.NewReader(jsonBody)
				requestURL := "http://localhost:8301/api/add"
				resp, err := http.NewRequest(http.MethodPost, requestURL, bodyReader)
				resp.Header.Set("Content-Type", "application/json")
				if err != nil {
					fmt.Println(err)
				} else {
					client := &http.Client{}
					response, err := client.Do(resp)
					if err != nil {
						fmt.Println(err)
					} else {
						fmt.Println(response)
					}
				}
				fmt.Print("Lost in the middle of no where\n")
				verifyString := `UPDATE userdata SET isverified = true WHERE dbid = $1`
				_, _ = db.Exec(verifyString, dbid)
				fmt.Println(isverified)

				responseMsg := Response{Msg: "Email Verified", Dbid: dbid}
				w.Header().Set("Content-Type", "application/json")
				w.WriteHeader(http.StatusOK)
				json.NewEncoder(w).Encode(responseMsg)
				return
			} else {
				responseMsg := Response{Msg: "Email already verified", Dbid: dbid}
				w.Header().Set("Content-Type", "application/json")
				w.WriteHeader(http.StatusOK)
				json.NewEncoder(w).Encode(responseMsg)
				return
			}
		}
		responseMsg := Response{Msg: "Invalid verification link", Dbid: dbid}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusForbidden)
		json.NewEncoder(w).Encode(responseMsg)
	} else {
		responseMsg := Response{Msg: "Method not allowed", Dbid: dbid}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusMethodNotAllowed)
		json.NewEncoder(w).Encode(responseMsg)
	}
}

// func temp(w http.ResponseWriter, r *http.Request) {
// 	fmt.Println(r.Method)

// 	w.Header().Set("Access-Control-Allow-Origin", "*")
// 	w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

// 	if r.Method == "GET" {
// 		dbid := "1"
// 		jsonBody := []byte(fmt.Sprintf(`{"dbid": "%s"}`, dbid))
// 		bodyReader := bytes.NewReader(jsonBody)
// 		requestURL := "http://localhost:8301/api/add"
// 		requ, _ := http.NewRequest(http.MethodPost, requestURL, bodyReader)
// 		requ.Header.Set("Content-Type", "application/json")

// 		// responseMsg := Response{Msg: "Email Verified", Dbid: "1"}
// 		// w.Header().Set("Content-Type", "application/json")
// 		// w.WriteHeader(http.StatusOK)
// 		// json.NewEncoder(w).Encode(responseMsg)
// 		// return
// 	} else {
// 		responseMsg := Response{Msg: "Method not allowed", Dbid: "1"}
// 		w.Header().Set("Content-Type", "application/json")
// 		w.WriteHeader(http.StatusMethodNotAllowed)
// 		json.NewEncoder(w).Encode(responseMsg)
// 	}
// }

func login(w http.ResponseWriter, r *http.Request) {
	fmt.Println(r.Method)

	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

	if r.Method == "POST" {

		body, _ := io.ReadAll(r.Body)
		keyVal := make(map[string]string)
		json.Unmarshal(body, &keyVal)
		email := keyVal["email"]
		pass := keyVal["password"]

		fmt.Printf("\n%s\n%s\n", email, pass)

		connStr := "postgres://postgres:password@localhost/postgres?sslmode=disable"
		db, err := sql.Open("postgres", connStr)

		if err != nil {
			panic(err)
		}
		err = db.Ping()
		if err != nil {
			panic(err)
		}

		queryString := `SELECT password, isverified, dbid FROM userdata WHERE email = $1;`
		row, _ := db.Query(queryString, email)

		for row.Next() {
			var password string
			var isverified string
			var dbid string
			_ = row.Scan(&password, &isverified, &dbid)
			if isverified == "false" {
				responseMsg := Response{Msg: "Email not verified", Dbid: dbid}
				w.Header().Set("Content-Type", "application/json")
				w.WriteHeader(http.StatusForbidden)
				json.NewEncoder(w).Encode(responseMsg)
				return
			}
			if pass == password {
				// cookie := http.Cookie{
				// 	Name:     "dbid",
				// 	Value:    dbid,
				// 	Path:     "/",

				// 	MaxAge:   3600,
				// 	HttpOnly: true,
				// 	Secure:   true,
				// 	SameSite: http.SameSiteLaxMode,
				// }
				cookie := http.Cookie{
					Name:     "example_cookie",
					Value:    "cookie_value",
					Path:     "/",
					Domain:   "localhost", // Replace with your actual domain
					HttpOnly: false,
					SameSite: http.SameSiteNoneMode,
					Secure:   false,
					// Secure:   true, // Set to true for HTTPS, false for HTTP
				}
				http.SetCookie(w, &cookie)
				responseMsg := Response{Msg: "Login Successful", Dbid: dbid}
				// w.Header().Set("Content-Type", "application/json")
				// w.Header().Set("Access-Control-Allow-Origin", "your_frontend_domain")
				// w.Header().Set("Access-Control-Allow-Credentials", "true")
				// w.Header().Set("Access-Control-Allow-Origin", "http://127.0.0.1:5500") // Replace with your frontend's actual origin
				// w.Header().Set("Access-Control-Allow-Credentials", "true")

				w.WriteHeader(http.StatusOK)
				json.NewEncoder(w).Encode(responseMsg)
				return

			} else {
				responseMsg := Response{Msg: "Incorrect Password", Dbid: dbid}
				w.Header().Set("Content-Type", "application/json")
				w.WriteHeader(http.StatusUnauthorized)
				json.NewEncoder(w).Encode(responseMsg)
				return
			}
		}
		responseMsg := Response{Msg: "Email id not found", Dbid: "-1"}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusForbidden)
		json.NewEncoder(w).Encode(responseMsg)
		return
	} else {
		responseMsg := Response{Msg: "Method not allowed", Dbid: "-1"}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusMethodNotAllowed)
		json.NewEncoder(w).Encode(responseMsg)
		return
	}
}

func main() {

	http.HandleFunc("/api/register/request", sendConfirmation)
	http.HandleFunc("/api/register/accept/", processConfirmation)
	http.HandleFunc("/api/login", login)

	err := http.ListenAndServe(":8101", nil)
	if err != nil {
		panic(err)
	}
}
