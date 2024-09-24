import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import {ApiService} from "../../../services/api.service";


@Component({
  selector: 'app-parametros',
  templateUrl: './parametros.component.html'
})
export class AppParametrosComponent implements OnInit {
  integracaoForm!: FormGroup;

  constructor(private fb: FormBuilder, private apiService: ApiService) {

  }

  ngOnInit(): void {
    // Initialize the form
    this.integracaoForm = this.fb.group({
      name: ['', Validators.required],
      forma_pagamento: ['', Validators.required],
      conta_contabil: ['', Validators.required],
      conta_contabil_contra_partida: ['', Validators.required],
      empresa: ['', Validators.required],
      cliente_tarifa: ['', Validators.required],
      cliente_frete: ['', Validators.required]
    });

    this.apiService.getIntegracaoData().subscribe((data: any) => {
      if (data) {
        this.integracaoForm.patchValue(data);
      }
    });
  }

  onSubmit(): void {
    if (this.integracaoForm.valid) {
      const formData = this.integracaoForm.value;
      this.apiService.submitIntegracaoData(formData).subscribe(response => {
        console.log('Form Submitted', response);
      });
    }
  }
}