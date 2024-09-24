import { Component } from '@angular/core';
import {FormGroup, FormControl, Validators, FormBuilder} from '@angular/forms';
import { Router } from '@angular/router';
import {ApiService} from "../../../services/api.service";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
})
export class AppSideRegisterComponent {

  registerForm: FormGroup;

  constructor(private router: Router, private fb: FormBuilder, private apiService: ApiService) {
    // Initialize the form with validation
    this.registerForm = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }

  onSubmit(): void {
    if (this.registerForm.valid) {
      const formData = this.registerForm.value;
      this.apiService.registerUser(formData).subscribe(
          response => {
            console.log('User registered successfully', response);
          },
          error => {
            console.error('Error registering user', error);
          }
      );
    }
  }
}
