import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import {SearchParameters} from "./search-parameters";
import {SearchStore} from "./search.store";
import {Subject} from "rxjs";


@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css'],
})
export class SearchComponent implements OnInit {
  error: any;
  // pagination settings
  private itemsPerPage: number = 10;
  maxSize: number = 5; // maxNumberButtonsVisible

  private searchParams: SearchParameters = new SearchParameters();
  private _searchParams: Subject<SearchParameters> = new Subject<SearchParameters>();

  constructor(
    private searchStore: SearchStore,
    private router: Router
  ) { }

  ngOnInit() {
    this.searchParams.language = 'de';
    this.searchParams.page = 1;
    this.searchParams.page_size = this.itemsPerPage;

    this._searchParams
      .debounceTime(300)        // wait for 300ms pause in events
      .distinctUntilChanged()   // ignore if next search term is same as previous
      .switchMap((v: any):any => {
        console.log(v);
        this.searchStore.search(this.searchParams);
        return v;
        // this.searchStore.search(searchParams);
      })
      .catch((error:any):any => {
        // TODO: real error handling
        console.log(error);
      });
    // this.executeSearch(null);
  }

  executeSearch(event:any): void {
    this.searchParams.page = 1;
    this.getMetadataList();
  }

  pageChanged(event:any): void {
    this.searchParams.page = event.page;
    this.getMetadataList();
  }

  private getMetadataList(): void {
    this._searchParams.next(this.searchParams);
    this.searchStore.search(this.searchParams);
  }

}
