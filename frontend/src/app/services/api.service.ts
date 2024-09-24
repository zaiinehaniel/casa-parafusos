import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import {API_URL} from "../constants";
import {Router} from "@angular/router";

@Injectable({
    providedIn: 'root'
})
export class ApiService {

    constructor(private http: HttpClient,  private router: Router) { }

    // Integracao Planilha
    submitFormData(formData: any): Observable<any> {
        const endpoint = API_URL + 'read_file';
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
        });
        return this.http.post<any>(endpoint, formData, { headers });
    }

    // Parametros
    submitIntegracaoData(formData: any): Observable<any> {
        const endpoint = API_URL + 'integracao';
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
        });
        return this.http.post<any>(endpoint, formData, { headers });
    }

    // Obter os parametros de integracao atuais
    getIntegracaoData(): Observable<any> {
        const endpoint = API_URL + 'integracao';
        return this.http.get<any>(endpoint);
    }

    // Cadastro Usuario
    registerUser(userData: any): Observable<any> {
        const endpoint = API_URL + 'users';  // API URL for the user registration endpoint
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
        });
        return this.http.post<any>(endpoint, userData, { headers });
    }

    // Login
// Submit login data to the backend API
    submitLoginData(formData: any): Observable<any> {
        const endpoint = API_URL + 'login';
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
        });

        return this.http.post<any>(endpoint, formData, { headers }).pipe(
            tap(response => {
                if (response && response.token) {
                    // Save token to localStorage
                    localStorage.setItem('authToken', response.token);
                }
            })
        );
    }

    // Check if user is logged in by verifying if token exists
    isLoggedIn(): boolean {
        return !!localStorage.getItem('authToken');
    }

    // Logout the user
    logout(): void {
        localStorage.removeItem('authToken');
        this.router.navigate(['/authentication/login']);
    }
}