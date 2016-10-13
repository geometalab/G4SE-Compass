import {isNullOrUndefined} from "util";

export class SearchParameters {
  search: string;
  language: string;
  ordering: string;
  limit: number;
  page_size: number;
  page: number;
  from_year: number;
  to_year: number;
  is_latest: boolean;

  loading: boolean = false; // to display spinner

  clear(): void {
    this.search = this.language = this.ordering = this.limit = this.page_size = this.page = this.is_latest = null;
  }

  private exists(value) {
    return (isNullOrUndefined(value)) || (value == '');
  }

  toUrlQuery(): string {
    var options_list: string[] = ["format=json"];

    if (!this.exists(this.search)){
      options_list.push('search=' + this.search);
    }
    if (!this.exists(this.language)){
      options_list.push('language=' + this.language);
    }
    if (!this.exists(this.ordering)){
      options_list.push('ordering=' + this.ordering);
    }
    if(!this.exists(this.limit)){
      options_list.push('limit=' + this.limit);
    }
    if(!this.exists(this.page_size)){
      options_list.push('page_size=' + this.page_size);
    }
    if(!this.exists(this.page)){
      options_list.push('page=' + this.page);
    }
    if(!this.exists(this.from_year)){
      options_list.push('from_year=' + this.from_year);
    }
    if(!this.exists(this.to_year)){
      options_list.push('to_year=' + this.to_year);
    }
    if(!this.exists(this.is_latest)){
      options_list.push('is_latest=' + this.is_latest);
    }
    var query_string = options_list.join('&');
    return '?' + query_string;
  }
}
