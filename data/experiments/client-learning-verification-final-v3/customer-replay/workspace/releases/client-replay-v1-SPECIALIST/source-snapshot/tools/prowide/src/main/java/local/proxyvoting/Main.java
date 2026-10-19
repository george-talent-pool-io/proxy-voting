package local.proxyvoting;
import com.google.gson.*;
import com.prowidesoftware.swift.model.*;
import com.prowidesoftware.swift.model.field.Field;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public final class Main {
 private static final Gson JSON=new Gson();
 private static Map<String,Object> parse(String text) throws Exception {
  Map<String,Object> out=new LinkedHashMap<>();out.put("parser","PROWIDE");out.put("dependency_version","SRU2025-10.3.20");out.put("standards_release","SRU2025");out.put("licence","Apache-2.0");out.put("adapter_version","prowide-jsonl-v1");out.put("raw_source",text);
  SwiftMessage message=SwiftMessage.parse(text);
  if(message==null||message.getBlock2()==null||message.getBlock4()==null)throw new IllegalArgumentException("FIN block2/block4 unavailable");
  out.put("message_type","MT"+message.getType());out.put("parse_status","PARSED_NOT_VALIDATED");out.put("standards_validated",false);
  List<Map<String,Object>> fields=new ArrayList<>();List<String> warnings=new ArrayList<>();List<String> stack=new ArrayList<>();
  for(Tag tag:message.getBlock4().getTags()){
   if(tag.getName().equals("16R"))stack.add(tag.getValue());
   Map<String,Object> value=new LinkedHashMap<>();value.put("tag",tag.getName());value.put("value",tag.getValue());value.put("sequence_path",new ArrayList<>(stack));value.put("source","PROWIDE");
   try {Field field=Field.getField(tag);if(field!=null){value.put("typed_field",field.getClass().getSimpleName());value.put("components",field.getComponents());}else value.put("unrecognised",true);}catch(Exception e){value.put("component_error",e.getClass().getSimpleName()+": "+e.getMessage());}
   fields.add(value);
   if(tag.getName().equals("16S")){
    if(!stack.isEmpty()&&stack.get(stack.size()-1).equals(tag.getValue()))stack.remove(stack.size()-1);else warnings.add("UNMATCHED_SEQUENCE_END:"+tag.getValue());
   }
  }
  if(!stack.isEmpty())warnings.add("UNCLOSED_SEQUENCES:"+stack.toString());
  out.put("fields",fields);out.put("warnings",warnings);
  out.put("validation_note","Prowide Core parsing is not SWIFT network/business-rule validation. No VALID ISO15022 claim is made from parse success alone.");return out;
 }
 public static void main(String[] args) throws Exception {
  BufferedReader in=new BufferedReader(new InputStreamReader(System.in,StandardCharsets.UTF_8));String line;
  while((line=in.readLine())!=null){
   Map<String,Object> result;
   try {JsonObject request=JsonParser.parseString(line).getAsJsonObject();String text=request.get("text").getAsString();if(text.length()>2000000)throw new IllegalArgumentException("Input limit");result=parse(text);}
   catch(Exception e){result=new LinkedHashMap<>();result.put("parser","PROWIDE");result.put("parse_status","FAILED");result.put("error",e.getClass().getSimpleName()+": "+e.getMessage());}
   System.out.println(JSON.toJson(result));System.out.flush();
  }
 }
}
