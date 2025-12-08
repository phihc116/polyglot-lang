use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, ItemFn, Expr, Token};
use syn::punctuated::Punctuated;

#[proc_macro_attribute]
pub fn route(args: TokenStream, input: TokenStream) -> TokenStream { 
    let args_parsed = 
    parse_macro_input!(args with Punctuated::<Expr, Token![,]>::parse_terminated);
    
    let func = parse_macro_input!(input as ItemFn);
 
    if args_parsed.len() != 2 { 
        return syn::Error::new_spanned(
            &args_parsed, 
            "The macro requires exactly two parameters: the Method and the Path. Example: #[route(GET, \"/api\")]"
        ).to_compile_error().into();
    }

    let method = &args_parsed[0];
    let path = &args_parsed[1];
 
    let fn_vis = &func.vis;
    let fn_sig = &func.sig;
    let fn_block = &func.block;
 
    let expanded = quote! {
        #fn_vis #fn_sig { 
            println!("--------------------------------------------------");
            println!("[Axum-Sim] Request: {} {}", stringify!(#method), #path);
            let start_time = std::time::Instant::now();
 
            println!("Executing Handler logic...");
            let result = {
                #fn_block
            };
 
            let duration = start_time.elapsed();
            println!("[200 OK] Completed in {:?}", duration);
            println!("--------------------------------------------------");

            result
        }
    };

    TokenStream::from(expanded)
}

#[proc_macro_derive(ToJson)]
pub fn derive_to_json(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as syn::DeriveInput);

    let name = &input.ident;
    
    let fields = if let syn::Data::Struct(data) = &input.data {
        if let syn::Fields::Named(fields) = &data.fields {
            fields
        } else {
             return syn::Error::new_spanned(
                name, 
                "ToJson only works on structs with named fields!"
            ).to_compile_error().into();
        }
    } else {
         return syn::Error::new_spanned(
            name, 
            "ToJson only works on structs!"
        ).to_compile_error().into();
    };

    let mut json_fields = Vec::new();
    for field in &fields.named {
        let field_name = &field.ident;
        json_fields.push(quote! {
            format!("\"{}\": \"{}\"", stringify!(#field_name), self.#field_name)
        });
    }

    let expanded = quote! {
        impl #name {
            pub fn to_json(&self) -> String {
                let mut json = String::from("{");
                let fields = vec![
                    #(#json_fields),*
                ];
                json.push_str(&fields.join(", "));
                json.push_str("}");
                json
            }
        }
    };

    TokenStream::from(expanded)
}