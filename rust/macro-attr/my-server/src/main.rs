#[macro_use] 
mod api_response;

use my_framework::{route, ToJson};
use std::thread;
use std::time::Duration;

#[route(GET, "/api/v1/health")]
fn health_check() { 
    let resp = api_response!(
        status => 200,
        message => "Server is healthy",
        uptime => "99.9%"
    );
    
    println!("(Return): {}", resp);
}

#[route(GET, "/api/v1/dashboard")]
fn dashboard_handler() { 
    thread::sleep(Duration::from_millis(150));
    println!("(Logic): Fetching revenue statistics...");
}

#[route(POST, "/api/v1/users")]
fn create_user() { 
    thread::sleep(Duration::from_millis(80));
    println!("(Logic): Inserting user into PostgreSQL database...");
    
    #[derive(ToJson)]
    struct User {
        id: u64,
        username: String,
        email: String,
    }

    let user = User {
        id: 1,
        username: "heron".to_string(),
        email: "herond.dev@gmail.com".to_string(),
    };

    println!("(Info): User created: {}", user.to_json());
}
 
fn main() {
    println!("Server Starting..."); 

    dashboard_handler();
    
    println!("\n... A moment later, another request arrives  ...\n");
    
    create_user();
}