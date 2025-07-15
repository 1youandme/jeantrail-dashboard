import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://jofycqthzpgjjnbvqcrx.supabase.co';
const supabaseAnonKey = 'ضع هنا الـ anon key'; // انسخه من Supabase

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
