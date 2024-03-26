export interface UserProfile {
  sub:string,
  full_name:string,
  family_name:string,
  given_name:string,
  email:string,
  name:string
}
export interface User {
  id: string;
  fullName: string;
  age: number;
  email: string;
  password: string;
  posts: Post[];
  createdAt: string;
  updatedAt: string;
  deletedAt: string;
}
export interface Post {
  id: number;
  title: string;
  content: string;
  likes: number;
  created_at: Date;
  updated_at: Date;
  deletedAt: Date;
  userId: number;
  userName: string;
}

export interface LoginResponse {
  token: string;
  user: User;
}
