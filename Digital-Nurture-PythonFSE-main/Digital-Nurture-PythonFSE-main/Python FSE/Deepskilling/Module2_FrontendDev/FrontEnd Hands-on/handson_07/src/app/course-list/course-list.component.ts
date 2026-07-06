import { Component, OnInit } from '@angular/core';
import { CourseService } from '../course.service';

@Component({
  selector: 'app-course-list',
  templateUrl: './course-list.component.html',
  styleUrls: ['./course-list.component.css']
})
export class CourseListComponent implements OnInit {
  courses: any[] = [];
  searchTerm: string = '';
  loading: boolean = true;
  error: string | null = null;

  constructor(private courseService: CourseService) { }

  ngOnInit(): void {
    this.loading = true;
    this.courseService.getCourses().subscribe({
      next: (data) => {
        this.courses = data;
        this.loading = false;
        this.error = null;
      },
      error: (err) => {
        console.error("HTTP error loading courses:", err);
        this.error = "Failed to load courses from API.";
        this.loading = false;
      }
    });
  }

  get filteredCourses(): any[] {
    const query = this.searchTerm.toLowerCase().trim();
    if (!query) return this.courses;
    
    return this.courses.filter(course => 
      course.name.toLowerCase().includes(query) || 
      course.code.toLowerCase().includes(query)
    );
  }

  trackByFn(index: number, item: any): number {
    return item.id;
  }
}
