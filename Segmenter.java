import java.io.IOException;
import java.io.StringReader;
import org.wltea.analyzer.core.IKSegmenter;
import org.wltea.analyzer.core.Lexeme;
import java.util.List;
import java.util.ArrayList;


public class Segmenter {
  private String text;
  public Segmenter(String text) {
     this.text = text;
  }
  public List<String> CutWord() {
    List<String> res = new ArrayList<String>();
    StringReader reader = new StringReader(this.text);
    IKSegmenter seg = new IKSegmenter(reader, true);
    Lexeme lex = new Lexeme(0, 0, 0, 0);
    try {
      while((lex=seg.next())!= null)
      {
	res.add(lex.getLexemeText());
      }
    } catch (IOException e) {
      e.printStackTrace();
    }
    return res;
  }
  public static void main(String[] args)
  {
    Segmenter w  = new Segmenter("这是薛宇的家，请好好爱护");
    List<String> a = w.CutWord();
    for (String s : a) {
      System.out.println(s);
    }
    
  }
}
