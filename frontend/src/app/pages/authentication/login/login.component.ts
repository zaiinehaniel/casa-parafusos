import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import {ApiService} from "../../../services/api.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
})
export class AppSideLoginComponent {
  loginForm: FormGroup;

  constructor(private fb: FormBuilder, private apiService: ApiService, private router: Router) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  onSubmit(): void {
    if (this.loginForm.valid) {
      const formData = this.loginForm.value;
      this.apiService.submitLoginData(formData).subscribe(
          response => {
            console.log('Login successful', response);
            // Redirect to '/extra/importacao' after login success
            this.router.navigate(['/extra/importacao']);
          },
          error => {
            console.error('Login failed', error);
            // Show error message (optional)
          }
      );
    }
  }
}
