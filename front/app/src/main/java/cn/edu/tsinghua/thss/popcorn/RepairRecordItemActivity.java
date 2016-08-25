package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.ImageView;
import android.widget.TextView;

import com.beardedhen.androidbootstrap.utils.ImageUtils;
import com.lidroid.xutils.BitmapUtils;
import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.view.annotation.ViewInject;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by 兜哥 on 2016/6/24.
 */
public class RepairRecordItemActivity extends Activity{
    @ViewInject(R.id.tv_title)
    private TextView tv_title;

    @ViewInject(R.id.tv_device_name)
    private  TextView tv_device_name;
    @ViewInject(R.id.tv_device_breif)
    private TextView tv_device_breif;
    @ViewInject(R.id.tv_creator)
    private TextView tv_creator;
    @ViewInject(R.id.tv_create_time)
    private TextView tv_create_time;
    @ViewInject(R.id.tv_editor)
    private TextView tv_editor;
    @ViewInject(R.id.tv_description)
    private TextView tv_description;
    @ViewInject(R.id.iv_image)
    private ImageView iv_image;

    @ViewInject(R.id.tv_memo)
    private TextView tv_memo;
    @ViewInject(R.id.tv_note)
    private TextView tv_note;
    private JSONObject task;

    public BitmapUtils bitmapUtils;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_repair_record_item);
        ViewUtils.inject(this);
        init();


    }

    private void init() {
        Intent intent=getIntent();
        Bundle bundle = intent.getExtras();
        try {
            task = new JSONObject(bundle.getString("task"));

        } catch (JSONException e) {
            e.printStackTrace();
        }
        setValueOfTextView();
    }

    private void setValueOfTextView() {
        String title="";
        String device_name="";
        String device_brief="";
        String creator="";
        String create_time="";
        String description="";
        String image="";String memo="";
        String editor="";
        String edit_datetime="";
        String note="";
        try {
            title=task.getString("title");
            device_brief=task.getString("device_brief");
            device_name=task.getString("device_name");
            creator=task.getString("creator");
            create_time=task.getString("create_time");
            description=task.getString("description");
            image=task.getString("image");
            memo=task.getString("memo");
            editor=task.getString("editor");
            edit_datetime=task.getString("edit_datetime");
            note=task.getString("note");
        } catch (JSONException e) {
            e.printStackTrace();
        }
        tv_title.setText(title);
        tv_device_breif.setText(device_brief);
        tv_device_name.setText(device_name);
        tv_creator.setText(creator);
        tv_create_time.setText(create_time);
        tv_description.setText(description);
//        iv_image.setText(image);
        bitmapUtils=new BitmapUtils(this);
        bitmapUtils.display(iv_image,"http://d.willwings.com/"+image);
//        System.out.println("=========="+image);
        tv_memo.setText(memo);
        tv_note.setText(note);
        tv_editor.setText(editor);



    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
    }
}
