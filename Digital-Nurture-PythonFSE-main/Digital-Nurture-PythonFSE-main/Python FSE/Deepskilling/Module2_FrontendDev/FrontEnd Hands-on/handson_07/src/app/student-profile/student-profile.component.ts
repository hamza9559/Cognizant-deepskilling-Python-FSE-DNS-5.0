import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-student-profile',
  templateUrl: './student-profile.component.html',
  styleUrls: ['./student-profile.component.css']
})
export class StudentProfileComponent implements OnInit {
  profileForm!: FormGroup;
  submittedData: any = null;

  constructor(private fb: FormBuilder) { }

  ngOnInit(): void {
    this.profileForm = this.fb.group({
      name: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      semester: ['', [Validators.required, Validators.min(1), Validators.max(8)]]
    });
  }

  onSubmit(): void {
    if (this.profileForm.valid) {
      console.log('Form Submitted!', this.profileForm.value);
      this.submittedData = this.profileForm.value;
      alert(`Profile Saved Successfully:\nName: ${this.submittedData.name}\nEmail: ${this.submittedData.email}\nSemester: ${this.submittedData.semester}`);
    }
  }

  // Helper getters for validation display
  get nameControl() {
    return this.profileForm.get('name');
  }

  get emailControl() {
    return this.profileForm.get('email');
  }

  get semesterControl() {
    return this.profileForm.get('semester');
  }
}
