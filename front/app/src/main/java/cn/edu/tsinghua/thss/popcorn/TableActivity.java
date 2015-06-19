package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Gravity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.json.JSONObject;

import cn.edu.tsinghua.thss.popcorn.QRcode.QRcodeActivity;
import cn.edu.tsinghua.thss.popcorn.formgenerator.FormActivity;


public class TableActivity extends FormActivity{
    static private int REQUEST_CODE = 2;
    private String  result;
    private TextView resultTextView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //generateForm{json)
        LinearLayout container = generateForm( FormActivity.parseFileToString( this, "schemas.json" ) );

        LinearLayout list = new LinearLayout(this);
        list.setGravity(Gravity.RIGHT);
        Button btn = new Button(this);
        resultTextView = new TextView(this);
        resultTextView.setGravity(Gravity.CENTER);
        btn.setText("签到");
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(TableActivity.this, QRcodeActivity.class);
                Bundle bundle = new Bundle();
                intent.putExtras(bundle);
                startActivityForResult(intent, REQUEST_CODE);
            }
        });

        list.addView(resultTextView);
        list.addView(btn);
        container.addView(list);



        Button submitBtn = new Button(this);
        submitBtn.setText("提交");
        submitBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                JSONObject json = save();
            }
        });
        container.addView(submitBtn);

        container.setPadding(20,20,20,20);
        setContentView(container);
    }

    /**
    * 处理回传值
    * 第二窗体返回值，在此方法中进行处理。
    */
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        // super.onActivityResult(requestCode, resultCode, data);
        //比对之前的请求编码，以及核对活动返回的编码是否是Activity.RESULT_OK
        if (Activity.RESULT_OK == resultCode && requestCode == REQUEST_CODE) {
            result = data.getStringExtra("result");
            resultTextView.setText(result);
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.table, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            TableActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
