import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { passwordMatchesValidator } from '../utils/password-matches';
import { RegisterStatus } from '../data-access/register.service';
import {Credentials} from "../../../models/credentials";

@Component({
  standalone: true,
  selector: 'app-register-form',
  imports: [
    ReactiveFormsModule
  ],
  templateUrl: './register-form.component.html',
  styleUrls: ['./register-form.component.scss']
})
export class RegisterFormComponent {
  @Input({ required: true }) status!: RegisterStatus;
  @Output() register = new EventEmitter<Credentials>();

  private fb = inject(FormBuilder);

  registerForm = this.fb.nonNullable.group(
    {
      email: ['', [Validators.email, Validators.required]],
      password: ['', [Validators.minLength(8), Validators.required]],
      confirmPassword: ['', [Validators.required]],
    },
    {
      updateOn: 'blur',
      validators: [passwordMatchesValidator],
    }
  );

  onSubmit() {
    if (this.registerForm.valid) {
      const { confirmPassword, ...credentials } =
        this.registerForm.getRawValue();
      this.register.emit(credentials);
    }
  }
}
