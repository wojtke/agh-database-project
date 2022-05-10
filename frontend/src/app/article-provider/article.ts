export interface Article{
  id: Number,
  title: String,
  tags: String[],
  category: String,
  content: String,
  imageSrc: String,
  grades: Number,
  sumGrades: Number,
  views: Number,
  addDate: Date
}

type util = {
  a1: string,
  s2: number,
  a3: number
}
export interface Quantity{
  quantity?:util,
  unit?:string
}
export interface Ingredient{
  name: string,
  quantity?:string
}
export interface Cocktail {
    id?: number,
    slug: string,
    name: string,
    ingredients?: Ingredient[],
    instructions?: string[],
    date_added?: Date
    date_updated?: Date
}

export interface Data{
  links: String[],

}
