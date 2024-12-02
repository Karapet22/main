import requests
import time
import random

BASE_URL = "https://new-api.example.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

def get_filtered_results():
    response = requests.get(f"{BASE_URL}/posts", headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        filtered_results = [
            post for post in data
            if len(post['title'].split()) <= 6 and post['body'].count('\n') <= 3
        ]
        print(f"Found {len(filtered_results)} posts after filtering.")
        return filtered_results
    else:
        print(f"Error fetching data: {response.status_code}")
        return []

def create_post():
    title = input("Enter post title: ")
    body = input("Enter post body: ")
    payload = {
        "title": title,
        "body": body,
        "userId": 1
    }
    response = requests.post(f"{BASE_URL}/posts", json=payload, headers=HEADERS)
    if response.status_code == 201:
        print("Post successfully created!")
        return response.json()
    else:
        print(f"Error creating post: {response.status_code}")
        return None

def update_post():
    post_id = input("Enter the ID of the post to update: ")
    title = input("Enter new title: ")
    body = input("Enter new body: ")
    payload = {
        "id": post_id,
        "title": title,
        "body": body,
        "userId": 1
    }
    response = requests.put(f"{BASE_URL}/posts/{post_id}", json=payload, headers=HEADERS)
    if response.status_code == 200:
        print("Post successfully updated!")
        return response.json()
    else:
        print(f"Error updating post: {response.status_code}")
        return None

def delete_post():
    post_id = input("Enter the ID of the post to delete: ")
    confirm = input(f"Are you sure you want to delete post with ID {post_id}? (yes/no): ")
    if confirm.lower() == "yes":
        response = requests.delete(f"{BASE_URL}/posts/{post_id}", headers=HEADERS)
        if response.status_code == 200:
            print(f"Post {post_id} successfully deleted.")
            return True
        else:
            print(f"Error deleting post: {response.status_code}")
            return False
    else:
        print("Delete action cancelled.")
        return False

def main():
    print("Welcome! Please choose an action:")
    while True:
        print("\n1. Get filtered results\n2. Create a new post\n3. Update a post\n4. Delete a post\n5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            time.sleep(random.uniform(1, 3)) 
            get_filtered_results()
        elif choice == "2":
            time.sleep(random.uniform(1, 3))
            create_post()
        elif choice == "3":
            time.sleep(random.uniform(1, 3))
            update_post()
        elif choice == "4":
            time.sleep(random.uniform(1, 3))
            delete_post()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
