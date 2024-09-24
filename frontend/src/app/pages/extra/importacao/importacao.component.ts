import { Component, OnInit } from '@angular/core';
import {FormControl, FormsModule, NgForm, Validators} from "@angular/forms";
import {ApiService} from "../../../services/api.service";

interface CustomFile extends File {
  base64: string;
  applicationType: string;
  fileName: string;
}

@Component({
  selector: 'app-importacao',
  templateUrl: './importacao.component.html'
})
export class AppImportacaoComponent implements OnInit {

  selectedPaymentGateway: any;
  files: CustomFile[] = [];
  paymentGateway: FormControl;
  file_need: boolean = false;
  model: any = {};

  constructor(
      private apiService: ApiService
  ) {
    this.paymentGateway = new FormControl('', Validators.required);
    this.file_need = false;
  }

  ngOnInit(): void {
    this.selectedPaymentGateway = 'mercadopago';
  }

  onDragOver(event: any) {
    event.preventDefault();
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    const files: FileList | null = event.dataTransfer?.files || null;
    if (files && files.length > 0) {
      this.processFiles(files);
    }
    this.validate_files_populated()
  }

  onFileSelected(event: any) {
    const files: FileList = event.target.files;
    if (files.length > 0) {
      this.processFiles(files);
    }
    this.validate_files_populated()
  }

  processFiles(files: FileList) {
    // Clear existing files array
    this.files = [];

    // Process the new file
    const file: CustomFile = files[0] as CustomFile;
    file.applicationType = file.type; // Assuming you want to use the file's MIME type as the application type
    file.fileName = file.name;
    this.generateBase64(file);
    this.files.push(file);
  }

  generateBase64(file: CustomFile) {
    const reader = new FileReader();
    reader.onload = () => {
      let base64String = reader.result as string;
      base64String = base64String.split(',')[1];
      file.base64 = base64String;
    };
    reader.readAsDataURL(file);
  }

  openFilePicker() {
    const fileInput = document.querySelector('input[type=file]') as HTMLElement;
    fileInput.click();
  }

  removeFile(selectedFileName: string) {
    this.files = this.files.filter(file => file.name !== selectedFileName);
  }
  submitForm(form: NgForm) {
    if (!this.file_need) {
      this.model = {
        'origem': this.selectedPaymentGateway,
        'file': this.files
      };
      // Call the submitFormData method of ApiService and subscribe to the Observable
      this.apiService.submitFormData(this.model).subscribe(
          (response: any) => {
            console.log('API response:', response);
          },
          (error: any) => {
            console.error('Error:', error);
          }
      );
      console.log(this.model);
    }
    this.validate_files_populated()
  }

  validate_files_populated() {
    this.file_need = this.files.length <= 0;
  }
}
