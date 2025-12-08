#[macro_export] 
macro_rules! api_response { 
    () => {
        String::from("{}")
    };

    ( $( $key:ident => $val:expr ),* ) => {
        {
            let mut json = String::from("{");
            let mut parts = Vec::new();
            
            $(
                parts.push(format!("\"{}\": \"{}\"", stringify!($key), $val));
            )*
             
            json.push_str(&parts.join(", "));
            json.push_str("}");
            json
        }
    };
}