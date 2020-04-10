#A partir de PDFs con tablas de la SSA, devuelve un CSV.

#Paquetería para leer pdfs y manipular fechas
using PDFIO
using Dates
using DelimitedFiles
using ArgParse

#Devuelve el texto del pdf como un string
function texto_pdf(archivo)

  #Abre el documento.
  documento = pdDocOpen(archivo)
  #Genera objetos que representan las páginas.
  pages = pdDocGetPageRange(documento, 1:pdDocGetPageCount(documento))
  #Creamos un buffer para compilar los datos.
  datos = IOBuffer()

  #Escribimos el texto al buffer.
  #Entre cada página forzamos una línea nueva.
  for page in pages
    pdPageExtractText(datos, page)
    write(datos, " \n")
  end

  #Cerramos el documento.
  pdDocClose(documento)

  #Devolvemos el texto en un string.
  return String(take!(datos))
end

#Separa el string por líneas y elimina aquellas que no corresponden a casos.
function eliminar_nocasos(string)

  #Separa por línea
  rows = split(string, "\n")
  #Revisa que el inicio de la línea sea de la forma {espacios}Número y descarta la línea si no.
  filter!(row -> occursin(r"^ +\d", row), rows)
  #Transforma los substrings en strings:
  rows = String.(rows)

  return rows
end


function procesa_fecha(string)
  try
    return Dates.format(Date(string, "dd/mm/yyyy"), "yyyy-mm-dd")
  catch e
    return ""
  end
end


function procesa_fila(string, index_fechas)
  out = replace(string, r"^\s+" => "")  # espacios al inicio
  out = replace(out, r"\s+$" => "")     # espacios al final

  # Correciones para normalizar una tabla como la de Abril 6
  correcciones = Dict("DISTRITO FEDERAL" => "CIUDAD DE MÉXICO",
                      "MEXICO" => "MÉXICO",
                      "MICHOACAN" => "MICHOACÁN",
                      "NUEVO LEON" => "NUEVO LEÓN",
                      "QUERETARO" => "QUERÉTARO",
                      "SAN LUIS POTOSI" => "SAN LUIS POTOSÍ",
                      "YUCATAN" => "YUCATÁN",
                      "MASCULINO" => "M",
                      "FEMENINO" => "F")

  for (k, v) in correcciones
    out = replace(out, k => v)
  end

  out = split(out, r"\s{2,}")           # mas de dos espacios define las entradas

  for i in index_fechas
    out[i] = procesa_fecha(out[i])  # fechas en formato ISO (de ser posible)
  end

  return out
end

#Función principal que toma el pdf y escribe csv correspondiente
function scraping(archivo_pdf, archivo_csv;
                  procedencia=false,
                  fecha_llegada=false,
                  index_fechas=[5])

  #Obtenemos los casos en un array:
  casos = procesa_fila.(eliminar_nocasos(texto_pdf(archivo_pdf)), Ref(index_fechas))
  # Ref evita el broadcasting con el segundo argumento (la lista de las columnas
  # que se tienen que considerar fechas)

  header = ["id", "estado", "sexo", "edad", "fecha_sintomas",
            "confirmacion"]  # "procedencia", fecha_llegada

  # Esto se puede cambiar para modificar el header
  procedencia ? push!(header, "procedencia") : nothing
  fecha_llegada ? push!(header, "fecha_llegada") : nothing

  #Escribe el archivo
  open(archivo_csv, "w") do io
    writedlm(io, [header], ',')
    writedlm(io, casos, ',')  # esto escribe todas las filas con separadores y \n
  end

  return "Done"
end

# Si el nombre del csv no se proporciona, se utiliza la misma base
function scraping(archivo_pdf; kwargs...)
  archivo_csv = splitext(basename(archivo_pdf))[1] * ".csv"
  scraping(archivo_pdf, archivo_csv; kwargs...)
end


function parse_commandline()
  settings = ArgParseSettings("convierte PDF con casos de covid-19 a archivo csv",
                              suppress_warnings=true)

  @add_arg_table! settings begin
    "pdf"
        help = "el archivo PDF con la tabla"
        required = true
    "--outfile", "-o"
        help = "el archivo csv donde se va a escribir el resultado (default: el nombre del PDF)"
        arg_type = String
        default = ""
    "--procedencia"
        help = "utilizar la columna `Procedencia` (default: falso)"
        action = :store_true
        default = false
    "--llegada"
        help = "utilizar la columna `Fecha de llegada a México` (default: falso)"
        action = :store_true
        default = false
  end

  return parse_args(ARGS, settings)
end

function main()
  parsed_args = parse_commandline()

  archivo_pdf = parsed_args["pdf"]
  @assert endswith(archivo_pdf, ".pdf")

  archivo_csv = parsed_args["outfile"]
  procedencia = parsed_args["procedencia"]
  fecha_llegada = parsed_args["llegada"]

  kwargs = Dict{Symbol,Any}()
  kwargs[:procedencia] = procedencia
  kwargs[:fecha_llegada] = fecha_llegada
  # trata de adivinar que fecha_llegada es una columna de fecha
  fecha_llegada ? kwargs[:index_fechas] = [5,8] : nothing

  if length(archivo_csv) == 0
    status = scraping(archivo_pdf; kwargs...)
  else
    @assert endswith(archivo_csv, ".csv")
    status = scraping(archivo_pdf, archivo_csv; kwargs...)
  end

  println(status)
end


if abspath(PROGRAM_FILE) == @__FILE__
  main()
end
