import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { Subject } from 'rxjs';

export enum NavigationDirection {
  FORWARD = 1,
  BACKWARD = -1
}
export class PaginationOpt {
  nextDisabled: boolean;
  previousDisabled: boolean;
  hidePerpage: boolean;
}
@Component({
  selector: 'app-page-pagination',
  templateUrl: './page-pagination.component.html',
  styleUrls: ['./page-pagination.component.scss']
})
export class PagePaginationComponent implements OnInit {
  @Input() paginationOpt : Subject<PaginationOpt>;
  @Output() navigate = new EventEmitter<NavigationDirection>();
  @Input() currentPage: number;
  // @Output() settings = new EventEmitter<PaginationOpt>();
  currentPaginationOpt: PaginationOpt = {
    nextDisabled: false,
    previousDisabled: true,
    hidePerpage: true,
  };
  constructor() { }

  ngOnInit() {
    this.paginationOpt.subscribe(data => {
      this.currentPaginationOpt = data;
    })
  }

  nav($e, direction) {
    $e.preventDefault();
    if (
      ($e.target.name == 'prev' && this.currentPaginationOpt.previousDisabled) ||
      ($e.target.name == 'next' && this.currentPaginationOpt.nextDisabled)
    )
      return;
    this.navigate.emit(direction);
  }

}
