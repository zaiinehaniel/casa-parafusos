import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import {ApiService} from "./services/api.service";

@Injectable({
    providedIn: 'root'
})
export class AuthGuard implements CanActivate {

    constructor(private apiService: ApiService, private router: Router) {}

    canActivate(): boolean {
        if (!this.apiService.isLoggedIn()) {
            // If user is not logged in, redirect to login page
            this.router.navigate(['/authentication/login']);
            return false;
        }
        return true;
    }
}
